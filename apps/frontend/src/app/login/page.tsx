"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  ShieldCheck, 
  Lock, 
  Mail, 
  ArrowRight, 
  Vote,
  ScanFace,
  Fingerprint
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'sonner'
import Link from 'next/link'

const LoginPage = () => {
  const [loading, setLoading] = useState(false)

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      toast.success("Login successful!", {
        description: "Welcome back to the National Voter Portal."
      })
    }, 1500)
  }

  return (
    <div className="min-h-screen bg-accent/30 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[30%] h-[30%] rounded-full bg-primary/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[30%] h-[30%] rounded-full bg-blue-500/10 blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md z-10">
        <div className="flex items-center justify-center gap-2 mb-8">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <Vote className="w-8 h-8 text-primary" />
            <h1 className="font-bold text-2xl tracking-tight">National Voter Portal</h1>
          </Link>
        </div>

        <Card className="shadow-2xl border-border/50 backdrop-blur-xl bg-background/80 overflow-hidden">
          <CardHeader className="text-center pb-2">
            <CardTitle className="text-2xl font-bold">Welcome Back</CardTitle>
            <CardDescription>Secure login to your electoral dashboard</CardDescription>
          </CardHeader>
          
          <CardContent className="pt-6">
            <Tabs defaultValue="password" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-8 h-12 p-1 bg-accent/50">
                <TabsTrigger value="password" name="password">Password</TabsTrigger>
                <TabsTrigger value="biometric" name="biometric">Biometric</TabsTrigger>
              </TabsList>
              
              <TabsContent value="password">
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input id="email" type="email" placeholder="name@example.com" className="pl-10 h-11" required />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <Label htmlFor="password">Password</Label>
                      <Link href="#" className="text-xs text-primary hover:underline">Forgot password?</Link>
                    </div>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input id="password" type="password" placeholder="••••••••" className="pl-10 h-11" required />
                    </div>
                  </div>
                  <Button type="submit" className="w-full h-12 text-lg rounded-xl shadow-lg shadow-primary/20" disabled={loading}>
                    {loading ? "Authenticating..." : "Login"}
                    {!loading && <ArrowRight className="ml-2 w-5 h-5" />}
                  </Button>
                </form>
              </TabsContent>
              
              <TabsContent value="biometric" className="space-y-6">
                <div className="grid grid-cols-1 gap-4">
                  <Button variant="outline" className="h-20 flex flex-col gap-1 border-2 hover:border-primary/50 group transition-all">
                    <ScanFace className="w-6 h-6 text-primary group-hover:scale-110 transition-transform" />
                    <span className="text-xs font-bold">Facial Recognition</span>
                  </Button>
                  <Button variant="outline" className="h-20 flex flex-col gap-1 border-2 hover:border-primary/50 group transition-all">
                    <Fingerprint className="w-6 h-6 text-primary group-hover:scale-110 transition-transform" />
                    <span className="text-xs font-bold">Fingerprint Scan</span>
                  </Button>
                </div>
                <div className="p-4 bg-primary/5 rounded-xl border border-primary/10 flex gap-3 text-left">
                  <ShieldCheck className="w-5 h-5 text-primary shrink-0" />
                  <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider">
                    Secure Multi-Factor Biometric Auth
                  </p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>

          <CardFooter className="bg-accent/20 border-t border-border/50 py-6">
            <p className="text-center w-full text-sm text-muted-foreground">
              Don&apos;t have a voter ID? <Link href="/register" className="text-primary font-bold hover:underline">Register now</Link>
            </p>
          </CardFooter>
        </Card>

        <div className="mt-8 flex justify-center gap-6 text-xs text-muted-foreground font-medium uppercase tracking-widest">
          <Link href="#" className="hover:text-foreground">Privacy Policy</Link>
          <Link href="#" className="hover:text-foreground">Terms of Service</Link>
          <Link href="#" className="hover:text-foreground">Support</Link>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
