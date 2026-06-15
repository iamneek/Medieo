import { Button } from "@/components/ui/button"
import Image from 'next/image'
import { HugeiconsIcon } from "@hugeicons/react"
import favicon from "./favicon.ico"
import { Upload01FreeIcons } from '@hugeicons/core-free-icons';

export default function Home() {
  return (
    <div className="flex flex-col flex-1 bg-zinc-50 font-sans dark:bg-black">
      <nav className="navbar flex justify-between items-center p-4">
        <div className="left_nav flex justify-center items-center gap-2">
          <Image src={favicon} alt="Icon" width={25} height={10} className="object-cover" />
          <h1 className="font-bold">Midieo</h1>
        </div>
        <div className="right_nav">
          <Button className="cursor-pointer">Upload <HugeiconsIcon icon={Upload01FreeIcons} size={32} color="#ffffff" strokeWidth={2} /></Button>
        </div>
      </nav>
    </div>
  );
}
