"use client"

import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ScanFace, 
  Fingerprint, 
  ShieldCheck, 
  Camera, 
  RotateCcw, 
  CheckCircle2,
  AlertCircle,
  Lock,
  Cpu
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { toast } from 'sonner'

const BiometricsPage = () => {
  const [scanning, setScanning] = useState(false)
  const [complete, setComplete] = useState(false)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Standby')

  const startScan = () => {
    setScanning(true)
    setComplete(false)
    setProgress(0)
    setStatus('Initializing AI...')
    
    // Simulate multi-stage scanning
    const intervals = [
      { p: 30, s: 'Detecting Face...' },
      { p: 60, s: 'Analyzing Liveness...' },
      { p: 85, s: 'Matching Embeddings...' },
      { p: 100, s: 'Authentication Success' }
    ]

    intervals.forEach((step, index) => {
      setTimeout(() => {
        setProgress(step.p)
        setStatus(step.s)
        if (step.p === 100) {
          setScanning(false)
          setComplete(true)
          toast.success("Identity Verified", {
            description: "Biometric authentication completed successfully."
          })
        }
      }, (index + 1) * 1000)
    })
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Biometric Center</h1>
        <p className="text-muted-foreground">Manage and verify your identity using AI-powered biometrics.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Verification Area */}
        <Card className="lg:col-span-2 border-border/50 overflow-hidden bg-background/50">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Facial Authentication</CardTitle>
                <CardDescription>Secure identity check using computer vision.</CardDescription>
              </div>
              <Badge variant="outline" className="text-primary border-primary/20 bg-primary/5">
                <Cpu className="w-3 h-3 mr-1" />
                AI Active
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="aspect-video bg-black relative flex items-center justify-center overflow-hidden">
              {/* Camera Simulation View */}
              {!complete ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-64 h-64 border-2 border-primary/30 rounded-full flex items-center justify-center">
                     <div className="w-48 h-48 border-2 border-primary/20 rounded-full border-dashed animate-spin-slow" />
                  </div>
                  {/* Scanning Line */}
                  {scanning && (
                    <motion.div 
                      className="absolute top-0 left-0 w-full h-1 bg-primary/50 shadow-[0_0_20px_rgba(var(--primary),0.5)] z-20"
                      animate={{ top: ['10%', '90%', '10%'] }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end justify-center pb-8">
                     <p className="text-white/80 font-bold tracking-widest uppercase text-xs">{status}</p>
                  </div>
                </div>
              ) : (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex flex-col items-center gap-4 text-primary"
                >
                  <div className="p-6 bg-primary/10 rounded-full">
                    <CheckCircle2 className="w-20 h-20" />
                  </div>
                  <p className="text-xl font-bold">Identity Confirmed</p>
                </motion.div>
              )}
            </div>
          </CardContent>
          <CardFooter className="p-6 flex justify-between bg-accent/10 border-t border-border/50">
            <div className="flex-1 mr-8">
              <div className="flex justify-between text-xs mb-2">
                <span className="text-muted-foreground">Verification Progress</span>
                <span className="font-bold">{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => { setComplete(false); setProgress(0); setStatus('Standby'); }}>
                <RotateCcw className="w-4 h-4 mr-2" />
                Reset
              </Button>
              <Button onClick={startScan} disabled={scanning || complete} className="shadow-lg shadow-primary/20">
                <Camera className="w-4 h-4 mr-2" />
                Start Scan
              </Button>
            </div>
          </CardFooter>
        </Card>

        {/* Info & Status */}
        <div className="space-y-6">
          <Card className="border-border/50 bg-background/50">
            <CardHeader>
              <CardTitle className="text-lg">Security Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between p-4 rounded-xl bg-green-500/5 border border-green-500/10">
                <div className="flex items-center gap-3">
                  <ScanFace className="w-5 h-5 text-green-500" />
                  <span className="text-sm font-medium">Face ID</span>
                </div>
                <Badge className="bg-green-500 hover:bg-green-500">Active</Badge>
              </div>
              <div className="flex items-center justify-between p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/10">
                <div className="flex items-center gap-3">
                  <Fingerprint className="w-5 h-5 text-yellow-500" />
                  <span className="text-sm font-medium">Fingerprint</span>
                </div>
                <Badge className="bg-yellow-500 hover:bg-yellow-500 text-[10px]">Setup Required</Badge>
              </div>
              <hr className="border-border/50" />
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <ShieldCheck className="w-4 h-4 text-primary mt-1" />
                  <div className="text-xs">
                    <p className="font-bold">Encrypted Vault</p>
                    <p className="text-muted-foreground mt-0.5 leading-relaxed">
                      Your biometrics are processed locally and stored as encrypted vectors.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Lock className="w-4 h-4 text-primary mt-1" />
                  <div className="text-xs">
                    <p className="font-bold">Privacy Guard</p>
                    <p className="text-muted-foreground mt-0.5 leading-relaxed">
                      We never store raw images or fingerprints on government servers.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/50 bg-primary/5 border-primary/20">
            <CardHeader>
              <CardTitle className="text-sm">Action History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { action: 'Login Verification', date: 'Oct 12, 14:22', result: 'Success' },
                  { action: 'Face Enrollment', date: 'Sep 30, 09:15', result: 'Success' },
                ].map((log, i) => (
                  <div key={i} className="flex justify-between items-center text-xs">
                    <div>
                      <p className="font-medium">{log.action}</p>
                      <p className="text-muted-foreground">{log.date}</p>
                    </div>
                    <span className="text-green-500 font-bold">{log.result}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default BiometricsPage
