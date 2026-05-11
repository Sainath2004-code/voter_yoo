"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  MapPin, 
  Search, 
  Navigation, 
  Info, 
  Clock, 
  Phone, 
  Accessibility,
  CheckCircle2,
  ExternalLink
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const booths = [
  { 
    id: 1, 
    name: 'Government Secondary School - Ward 4', 
    address: '12/B Sector 4, New Delhi, 110001', 
    distance: '0.8 km',
    status: 'Open',
    queueTime: '15 mins',
    accessibility: true,
    coordinates: { lat: 28.6139, lng: 77.2090 }
  },
  { 
    id: 2, 
    name: 'Community Center - Block C', 
    address: 'Near Metro Station, New Delhi, 110005', 
    distance: '2.4 km',
    status: 'Open',
    queueTime: '45 mins',
    accessibility: true,
    coordinates: { lat: 28.6239, lng: 77.2190 }
  },
  { 
    id: 3, 
    name: 'Public Library Annex', 
    address: 'Main Market Road, New Delhi, 110008', 
    distance: '3.1 km',
    status: 'Busy',
    queueTime: '1.5 hours',
    accessibility: false,
    coordinates: { lat: 28.6339, lng: 77.2290 }
  },
]

const BoothLocator = () => {
  const [selectedBooth, setSelectedBooth] = useState(booths[0])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Polling Booth Locator</h1>
        <p className="text-muted-foreground">Find your assigned polling station and check live queue status.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: List & Search */}
        <div className="space-y-6">
          <Card className="border-border/50 bg-background/50">
            <CardHeader className="pb-4">
              <div className="relative">
                <Search className="absolute left-3 top-2.5 w-4 h-4 text-muted-foreground" />
                <Input placeholder="Enter your Zip or Area..." className="pl-10 rounded-xl" />
              </div>
            </CardHeader>
            <CardContent className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
              {booths.map((booth) => (
                <div 
                  key={booth.id}
                  onClick={() => setSelectedBooth(booth)}
                  className={cn(
                    "p-4 rounded-2xl cursor-pointer transition-all border-2",
                    selectedBooth.id === booth.id 
                      ? "bg-primary/5 border-primary/30" 
                      : "bg-accent/20 border-transparent hover:border-border/50"
                  )}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-bold text-sm leading-tight">{booth.name}</h4>
                    <span className="text-[10px] font-bold text-primary shrink-0">{booth.distance}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground mb-3">
                    <MapPin className="w-3 h-3" />
                    {booth.address}
                  </div>
                  <div className="flex gap-2">
                    <Badge variant="outline" className={cn(
                      "text-[10px] border-none",
                      booth.status === 'Open' ? "bg-green-500/10 text-green-500" : "bg-yellow-500/10 text-yellow-500"
                    )}>
                      {booth.status}
                    </Badge>
                    <Badge variant="outline" className="text-[10px] bg-primary/5 text-primary border-none">
                      <Clock className="w-3 h-3 mr-1" />
                      {booth.queueTime}
                    </Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Right: Map Simulation & Details */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-border/50 bg-background/50 overflow-hidden h-[400px] relative group">
            {/* Map Simulation Placeholder */}
            <div className="absolute inset-0 bg-accent/30 flex items-center justify-center">
              <div className="relative w-full h-full overflow-hidden opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,rgba(var(--background),0.8)_100%)] z-10" />
                {/* Simulated Map Grid */}
                <div className="grid grid-cols-12 grid-rows-12 h-full w-full">
                  {Array.from({ length: 144 }).map((_, i) => (
                    <div key={i} className="border-[0.5px] border-primary/10" />
                  ))}
                </div>
              </div>
              {/* Floating Pin */}
              <motion.div 
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute z-20 flex flex-col items-center"
              >
                <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center shadow-2xl shadow-primary/50 border-4 border-background">
                  <MapPin className="w-6 h-6 text-primary-foreground" />
                </div>
                <div className="w-2 h-2 bg-primary/50 blur-sm rounded-full mt-2" />
              </motion.div>

              <div className="absolute bottom-6 right-6 z-30 flex gap-2">
                <Button size="sm" className="rounded-full shadow-lg">
                  <Navigation className="w-4 h-4 mr-2" />
                  Navigate
                </Button>
                <Button size="sm" variant="secondary" className="rounded-full shadow-lg">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  View Larger
                </Button>
              </div>
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="border-border/50 bg-background/50">
              <CardHeader>
                <CardTitle className="text-lg">Station Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-primary mt-1" />
                  <div>
                    <p className="text-xs font-bold text-muted-foreground uppercase">Booth ID</p>
                    <p className="font-bold">ND-DL-004-C</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Phone className="w-5 h-5 text-primary mt-1" />
                  <div>
                    <p className="text-xs font-bold text-muted-foreground uppercase">Station In-charge</p>
                    <p className="font-bold">+91 98765-43210</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Accessibility className="w-5 h-5 text-primary mt-1" />
                  <div>
                    <p className="text-xs font-bold text-muted-foreground uppercase">Accessibility</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className="bg-green-500/10 text-green-500 border-none">Wheelchair Ramp</Badge>
                      <Badge className="bg-green-500/10 text-green-500 border-none">Voice Guide</Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50 bg-primary/5 border-primary/20">
              <CardHeader>
                <CardTitle className="text-lg">Voter Assignment</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="p-4 bg-background/80 rounded-2xl border border-border/50 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="w-5 h-5 text-primary" />
                    <span className="text-sm font-medium">Assigned to this booth</span>
                  </div>
                  <Badge className="bg-primary/10 text-primary border-none">Confirmed</Badge>
                </div>
                <p className="text-[11px] text-muted-foreground leading-relaxed italic">
                  Note: Please bring your Digital Voter ID and one national identity proof on election day. Biometric verification will be required at the entrance.
                </p>
                <Button className="w-full rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground font-bold h-12">
                  Download Polling Pass
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

import { cn } from '@/lib/utils'

export default BoothLocator
