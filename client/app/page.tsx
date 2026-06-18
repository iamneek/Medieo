"use client"

import axios from 'axios';
import { useEffect, useState } from 'react';

export default function Home() {
  const get_vids = async () => {
    let vids = await axios.get("http://127.0.0.1:8000/");
    console.log(vids.data.videos);
  }
  useEffect(() => { get_vids() }, [])

  return (
    <div className="flex flex-col flex-1 font-sans dark:bg-black">

    </div>
  );
}
