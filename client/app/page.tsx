"use client"

import axios from 'axios';
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [vids, setVids] = useState([]);
  const get_vids = async () => {
    let vids = await axios.get("http://127.0.0.1:8000/");
    setVids(vids.data.videos);
  }
  useEffect(() => { get_vids() }, [])

  return (
    <div className="flex-1 px-4 md:px-6 py-6 bg-white dark:bg-black">
      <h1 className="text-3xl font-bold mb-8">Explore</h1>

      <div
        className="
        grid
        grid-cols-1
        sm:grid-cols-2
        md:grid-cols-3
        lg:grid-cols-4
        xl:grid-cols-5
        gap-x-4
        gap-y-8
      "
      >
        {vids.map((vid: any) => (
          <Link
            key={vid.upload_id}
            href={`/watch/${vid.upload_id}`}
            className="group"
          >
            <div className="overflow-hidden rounded-xl">
              <img
                src={"https://placehold.co/1280x720/png?text=Thumbnail"}
                alt={vid.title}
                className="
                w-full
                aspect-video
                object-cover
                transition-transform
                duration-300
                group-hover:scale-105
              "
              />
            </div>


            <div className="flex mt-3 gap-3">

              <div className="flex-shrink-0">
                <div className="w-9 h-9 rounded-full bg-gray-300 dark:bg-gray-700" />
              </div>

              <div className="min-w-0">
                <h3 className="font-medium text-sm text-black dark:text-white line-clamp-2">
                  {vid.title}
                </h3>

                <p className="text-xs text-gray-500 dark:text-gray-500">
                  {new Date(vid.uploaded_at).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
