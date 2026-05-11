"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { 
  Users, 
  ShieldCheck, 
  MapPin, 
  TrendingUp, 
  Flag,
  AlertTriangle,
  Building2,
  FileText
} from 'lucide-react'
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const stats = [
  { title: 'Total Electors', value: '96.8 Cr', sub: 'Across 28 States', icon: Users },
  { title: 'EPIC Generated', value: '94.2 Cr', sub: '97% Coverage', icon: ShieldCheck },
  { title: 'Polling Booths', value: '10.5 Lakh', sub: 'Active Stations', icon: MapPin },
  { title: 'BLO Verified', value: '88%', sub: 'Field Verification', icon: Flag },
]

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const ECIDashboard = () => {
  return (
    <div className="space-y-8 p-2">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Chief Electoral Officer Dashboard</h1>
          <p className="text-muted-foreground italic">Vahan Voter Management System • Election Commission of India</p>
        </div>
        <div className="flex gap-3">
          <Select defaultValue="national">
            <SelectTrigger className="w-[180px] rounded-xl">
              <SelectValue placeholder="Select State" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="national">All India</SelectItem>
              <SelectItem value="MH">Maharashtra</SelectItem>
              <SelectItem value="UP">Uttar Pradesh</SelectItem>
              <SelectItem value="TN">Tamil Nadu</SelectItem>
            </SelectContent>
          </Select>
          <Button className="bg-primary text-primary-foreground shadow-lg shadow-primary/20">
            Generate ECI Report
          </Button>
        </div>
      </div>

      {/* Indian Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card className="border-border/50 bg-background/50 border-l-4 border-l-primary shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-2 bg-primary/5 rounded-full text-primary">
                    <stat.icon className="w-5 h-5" />
                  </div>
                  <Badge variant="outline" className="text-[10px] uppercase font-bold tracking-widest text-primary border-primary/20 bg-primary/5">
                    Live
                  </Badge>
                </div>
                <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-tight">{stat.title}</h3>
                <p className="text-3xl font-black mt-1">{stat.value}</p>
                <p className="text-xs text-muted-foreground mt-1">{stat.sub}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Registration Map View */}
        <Card className="lg:col-span-2 border-border/50 bg-background/50">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Regional Registration Intensity</CardTitle>
              <CardDescription>Live heat-map of voter registrations across Districts.</CardDescription>
            </div>
            <div className="p-2 bg-accent/50 rounded-lg">
               <TrendingUp className="w-4 h-4 text-primary" />
            </div>
          </CardHeader>
          <CardContent className="h-[400px] flex items-center justify-center bg-accent/10 rounded-xl m-6 border border-dashed border-border/50 relative overflow-hidden">
             {/* Map Placeholder */}
             <div className="text-center space-y-4 z-10">
                <Building2 className="w-16 h-16 text-muted-foreground/30 mx-auto" />
                <p className="text-sm text-muted-foreground font-medium">Interactive India GeoJSON Map Loading...</p>
                <Button variant="outline" size="sm">Reload PostGIS Data</Button>
             </div>
             {/* Background Decoration */}
             <div className="absolute inset-0 opacity-5 pointer-events-none">
                <div className="grid grid-cols-10 grid-rows-10 h-full w-full">
                    {Array.from({ length: 100 }).map((_, i) => (
                        <div key={i} className="border border-primary/20" />
                    ))}
                </div>
             </div>
          </CardContent>
        </Card>

        {/* Right: Security & Compliance */}
        <div className="space-y-6">
          <Card className="border-border/50 bg-background/50">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-primary" />
                Compliance Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                { label: 'DPDP Privacy Protocol', value: 'Active', color: 'green' },
                { label: 'Aadhaar Vault Sync', value: '99.9%', color: 'green' },
                { label: 'Biometric Encryption', value: 'AES-256', color: 'green' },
                { label: 'Audit Log Integrity', value: 'Verified', color: 'green' },
              ].map((item, i) => (
                <div key={i} className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">{item.label}</span>
                  <Badge className="bg-green-500/10 text-green-500 border-none">{item.value}</Badge>
                </div>
              ))}
              <hr className="border-border/50" />
              <div className="p-4 bg-yellow-500/5 border border-yellow-500/20 rounded-xl">
                 <div className="flex items-center gap-2 text-yellow-600 mb-2">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-xs font-bold uppercase">Security Advisory</span>
                 </div>
                 <p className="text-[10px] text-muted-foreground leading-relaxed">
                    Detected anomalous EPIC lookup attempts from restricted IP range. WAF firewall rules updated.
                 </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/50 bg-primary/5 border-primary/20">
            <CardHeader>
              <CardTitle className="text-sm">Administrative Hierarchy</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">States Registered</span>
                  <span className="font-bold">28 / 28</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">Districts Active</span>
                  <span className="font-bold">766 / 766</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">Constituencies (LS)</span>
                  <span className="font-bold">543</span>
                </div>
                <Button className="w-full mt-2 rounded-xl text-xs h-9" variant="outline">
                   Manage Hierarchy
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default ECIDashboard
