// components/upload-progress.tsx
import { cn } from "@/lib/utils"

interface UploadProgressProps {
    progress: number
    isUploaded: boolean
}

export default function UploadProgress({ progress, isUploaded }: UploadProgressProps) {
    if (progress === 0) return null

    return (
        <div className="flex flex-col gap-1 w-full">
            <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                <div
                    className={cn(
                        "h-full rounded-full transition-all duration-300",
                        isUploaded ? "bg-green-500" : "bg-primary"
                    )}
                    style={{ width: `${progress}%` }}
                />
            </div>
            <p className="text-xs text-muted-foreground text-right">
                {isUploaded ? "Upload complete" : `${progress}%`}
            </p>
        </div>
    )
}