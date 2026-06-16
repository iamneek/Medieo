"use client"

import { Button } from "@/components/ui/button"
import Image from 'next/image'
import { HugeiconsIcon } from "@hugeicons/react"
import favicon from "@/app/favicon.ico"
import { Upload01FreeIcons } from '@hugeicons/core-free-icons';
import { useRouter } from "next/navigation";
import Link from "next/link"

export default function Navbar() {
    const router = useRouter();
    return (<nav className="navbar flex justify-between items-center p-4">
        <Link href={"/"}>
            <div className="left_nav flex justify-center items-center gap-2">
                <Image src={favicon} alt="Icon" width={25} height={10} className="object-cover" />
                <h1 className="font-bold">Midieo</h1>
            </div>
        </Link>
        <div className="right_nav">
            <Button className="cursor-pointer" onClick={() => router.push("/upload")}>Upload <HugeiconsIcon icon={Upload01FreeIcons} size={32} color="#ffffff" strokeWidth={2} /></Button>
        </div>
    </nav>)
}