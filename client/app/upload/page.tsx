"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect, useRef } from "react"
import { Upload01FreeIcons } from '@hugeicons/core-free-icons';
import { HugeiconsIcon } from "@hugeicons/react"
import { cn } from "@/lib/utils";
import axios from 'axios';
import UploadProgress from "@/components/Upload-Progress"

export default function Upload() {
    const [file, setFile] = useState<File | null>(null);
    const [progress, SetProgress] = useState<number>(0);
    const [isUploaded, setUploaded] = useState<boolean>(false);
    const [taskId, setTaskId] = useState<string | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | Blob | MediaSource | MediaStream | undefined>();

    const fileInputRef = useRef<HTMLInputElement>(null)
    const titleInputRef = useRef<HTMLInputElement>(null)
    const descInputRef = useRef<HTMLInputElement>(null)


    useEffect(() => {
        if (fileInputRef.current) fileInputRef.current.value = ""
    }, [])

    const handleImage = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            setPreviewUrl(URL.createObjectURL(selectedFile));
        }
    }

    const handleUpload = async (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.preventDefault()
        const title_value = titleInputRef.current?.value
        const desc_value = descInputRef.current?.value
        const response = await axios.post('http://127.0.0.1:8000/upload/init')
        const upload_id = response.data.upload_id
        const chunk_size = 1024 * 1024
        let offset = 0
        let current_chunk = 0
        let file_resp
        if (file) {
            while (offset < file?.size) {
                const chunk = file.slice(offset, offset + chunk_size);
                const chunk_blob = new Blob([chunk], { type: file.type })
                const formData = new FormData()
                formData.append("up_id", upload_id)
                if (title_value) {
                    formData.append("video_title", title_value)
                } else {
                    console.log("No video title")
                    return;
                }
                if (desc_value) {
                    formData.append("video_description", desc_value)
                }
                formData.append("chunk_num", String(current_chunk))
                formData.append("chunks", chunk_blob)
                formData.append("total_chunks", String(Math.ceil(file?.size / chunk_size)))
                file_resp = await axios.post('http://127.0.0.1:8000/upload/', formData)
                offset += chunk_size
                current_chunk += 1
                SetProgress(Math.round((offset / file.size) * 100))
            }
            const taskID = file_resp?.data.task_id
            setTaskId(taskID)
            setUploaded(true)
            SetProgress(0)
            console.log("offset: ", offset)
            console.log("file size: ", file?.size)
            console.log("Task ID: ", taskID)
        }
    }

    return (
        <div className="flex flex-col flex-1 justify-center items-center font-sans dark:bg-black">
            <form action="" className="flex flex-col gap-2 w-[50vw]">
                <video
                    id="preview-img"
                    src={previewUrl}
                    className={cn("object-contain max-h-full max-w-full", !file && "hidden")}
                />
                <Input type="text" placeholder="Video Title" name="video_title" ref={titleInputRef} />
                <Input type="text" placeholder="Video Description" className="py-7" ref={descInputRef} />
                <Input type="file" id="upload_input" accept=".mp4, .mkv, .mov" onChange={(e) => handleImage(e)} ref={fileInputRef} />
                <Button className="mt-4" onClick={(e) => handleUpload(e)} disabled={progress > 0}>Upload <HugeiconsIcon icon={Upload01FreeIcons} size={32} color="#ffffff" strokeWidth={2} /></Button>
                <UploadProgress progress={progress} isUploaded={isUploaded} />
            </form>
        </div>
    )
}