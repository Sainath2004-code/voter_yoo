"use client"

import React from 'react'
import { MapPin, Info } from 'lucide-react'
import { motion } from 'framer-motion'

interface MapProps {
    center?: [number, number];
    zoom?: number;
    title?: string;
}

const MapComponent = ({ title = "Regional Boundary Viewer" }: MapProps) => {
  return (
    <div className="relative w-full h-full bg-accent/20 rounded-2xl border border-border/50 overflow-hidden group">
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10" />
      
      {/* Simulated Map Markers */}
      <motion.div 
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ duration: 3, repeat: Infinity }}
        className="absolute top-1/4 left-1/3 z-10"
      >
        <MapPin className="w-8 h-8 text-primary shadow-2xl" />
      </motion.div>

      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-0 opacity-20 pointer-events-none">
         {/* Simulated Boundary Polygon */}
         <div className="w-[300px] h-[300px] bg-primary rounded-[30% 70% 70% 30% / 30% 30% 70% 70%] animate-pulse" />
      </div>

      {/* Map UI Overlay */}
      <div className="absolute top-4 left-4 z-20">
         <div className="bg-background/80 backdrop-blur-md p-3 rounded-xl border border-border/50 shadow-xl">
            <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{title}</p>
            <p className="text-xs font-bold mt-1">Status: PostGIS Connected</p>
         </div>
      </div>

      <div className="absolute bottom-4 right-4 z-20 flex flex-col gap-2">
         <div className="bg-background/80 backdrop-blur-md p-2 rounded-xl border border-border/50 shadow-xl">
            <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-primary rounded-sm" />
                <span className="text-[10px] font-medium">High Density Area</span>
            </div>
         </div>
         <div className="bg-background/80 backdrop-blur-md p-2 rounded-xl border border-border/50 shadow-xl">
            <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-accent rounded-sm" />
                <span className="text-[10px] font-medium">Rural Zones</span>
            </div>
         </div>
      </div>

      <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity">
         <div className="bg-primary/10 backdrop-blur-sm px-6 py-3 rounded-full border border-primary/20 flex items-center gap-2">
            <Info className="w-4 h-4 text-primary" />
            <span className="text-xs font-bold text-primary uppercase tracking-widest">PostGIS Boundary Data Layer</span>
         </div>
      </div>
    </div>
  )
}

export default MapComponent
