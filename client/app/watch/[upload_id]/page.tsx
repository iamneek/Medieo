"use client"

import axios from 'axios'
import { use, useEffect, useState, useRef } from 'react'
import Hls from "hls.js"

export default function Watch({ params }: { params: Promise<{ upload_id: string }> }) {
    const { upload_id } = use(params)
    const [source, setSource] = useState<string>("")
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => { getPresignedUrl() }, [])

    useEffect(() => {
        const vid = videoRef.current
        if (!vid) return

        let hls: Hls;

        if (Hls.isSupported()) {
            hls = new Hls()
            hls.loadSource(source)
            hls.attachMedia(vid)
            hls.on(Hls.Events.MANIFEST_PARSED, () => {
                console.log("Ready to play")
            });

            hls.on(Hls.Events.MANIFEST_PARSED, async () => {
                try {
                    await vid.play();
                } catch (err) {
                    console.log("Autoplay blocked:", err);
                }
            });
        }

        return () => {
            if (hls) {
                hls.destroy()
            }
        }
    }, [source])

    const getPresignedUrl = async () => {
        const resp = await axios.get(`http://127.0.0.1:8000/watch/${upload_id}`)
        const stream_url = resp.data.stream_url
        setSource(stream_url)
    }
    return (
        <div className="flex w-full items-center justify-center">
            <video ref={videoRef} controls playsInline className="w-[80%] mt-10 bg-black"></video>
        </div>
    )
}