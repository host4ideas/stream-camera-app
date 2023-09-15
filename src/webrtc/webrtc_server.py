# Core
import json
import logging
import os
import platform
import ssl
# Libraries
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaStreamTrack
# Utils
from utils.utils import Args, RTCOfferRequest
from utils.background_filters import blur_background
# Types
from av import VideoFrame
from typing import Callable
from cv2.typing import MatLike

ROOT = os.path.dirname(__file__)

# https://dev.to/whitphx/python-webrtc-basics-with-aiortc-48id
# https://github.com/aiortc/aiortc/blob/2362e6d1f0c730a0f8c387bbea76546775ad2fe8/examples/server/server.py
# https://pyav.org/docs/9.0.2/api/video.html


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track: MediaStreamTrack, transform):
        super().__init__()  # don't forget this to inherit from MediaStreamTrack!
        self.track = track
        self.transform = transform

    def apply_filter(self, frame: VideoFrame, filter_fn: Callable[[MatLike]]):
        # VideoFrame to numpy array
        img = frame.to_ndarray(format="bgr24")
        # Apply filter
        img = filter_fn(img)
        # rebuild a VideoFrame from numpy array, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame

    async def recv(self):
        # Fetch next frame
        frame = await self.track.recv()
        if self.transform == "blur_background":
            return self.apply_filter(frame, blur_background)
        else:
            return frame


class RTCServer:
    def __init__(self, args: Args):
        self.args = args
        self.pcs: set[RTCPeerConnection] = set()

    async def offer(self, request: RTCOfferRequest):
        params: RTCOfferRequest = await request.json()
        offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        # Camera source
        options = {"framerate": "30", "video_size": "640x480"}
        if platform.system() == "Darwin":
            player = MediaPlayer(
                "default:none", format="avfoundation", options=options
            )
        elif platform.system() == "Windows":
            player = MediaPlayer(
                "video=Integrated Camera", format="dshow", options=options
            )
        else:
            player = MediaPlayer("/dev/video0", format="v4l2", options=options)

        await pc.setRemoteDescription(offer)
        for t in pc.getTransceivers():
            if t.kind == "audio" and player.audio:
                pc.addTrack(player.audio)
            elif t.kind == "video" and player.video:
                # Transform frame with opencv
                local_video = VideoTransformTrack(
                    player.audio, transform=params.video_transform
                )
                pc.addTrack(local_video)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )

    async def on_shutdown(self, app: web.Application):
        # close peer connections
        coros = [pc.close() for pc in self.pcs]
        await asyncio.gather(*coros)
        self.pcs.clear()

    def main(self):
        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)

        if self.args.cert_file:
            ssl_context = ssl.SSLContext()
            ssl_context.load_cert_chain(
                self.args.cert_file, self.args.key_file)
        else:
            ssl_context = None

        app = web.Application()
        app.on_shutdown.append(self.on_shutdown)
        app.router.add_post("/offer", self.offer)
        web.run_app(app, host=self.args.host, port=self.args.port,
                    ssl_context=ssl_context)
