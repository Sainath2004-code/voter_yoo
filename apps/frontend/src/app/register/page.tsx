"use client"

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  User, 
  IdCard, 
  ScanFace, 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft,
  Vote,
  ShieldCheck,
  Building2,
  FileText
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { toast } from 'sonner'
import Link from 'next/link'

const steps = [
  { id: 1, title: 'Personal', icon: <User className="w-5 h-5" /> },
  { id: 2, title: 'Address', icon: <Building2 className="w-5 h-5" /> },
  { id: 3, title: 'Biometrics', icon: <ScanFace className="w-5 h-5" /> },
  { id: 4, title: 'Complete', icon: <CheckCircle2 className="w-5 h-5" /> },
]

const Form6Registration = () => {
  const [currentStep, setCurrentStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    fullName: '',
    fatherName: '',
    dob: '',
    gender: '',
    aadhaar: '',
    state: '',
    district: '',
    constituency: '',
    pincode: ''
  })

  const handleNext = () => {
    if (currentStep < 4) {
      setLoading(true)
      setTimeout(() => {
        setLoading(false)
        setCurrentStep(currentStep + 1)
      }, 800)
    }
  }

  return (
    <div className="min-h-screen bg-accent/30 flex items-center justify-center p-4 py-20 relative overflow-hidden">
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-primary/10 blur-[120px] pointer-events-none" />
      
      <div className="w-full max-w-2xl z-10">
        <div className="flex flex-col items-center gap-2 mb-8">
            <div className="p-3 bg-primary rounded-2xl shadow-lg shadow-primary/20">
               <Vote className="w-8 h-8 text-primary-foreground" />
            </div>
            <h1 className="font-black text-2xl tracking-tight text-center">ELECTION COMMISSION OF INDIA</h1>
            <Badge variant="outline" className="border-primary/20 bg-primary/5 text-primary">National Voter Service Portal</Badge>
        </div>

        <Card className="shadow-2xl border-border/50 backdrop-blur-xl bg-background/80 overflow-hidden rounded-3xl">
          <div className="h-1.5 bg-muted">
            <motion.div 
              className="h-full bg-primary" 
              initial={{ width: '25%' }}
              animate={{ width: `${(currentStep / 4) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          
          <CardHeader className="space-y-6 pb-2">
            <div className="flex justify-between items-center px-4">
              {steps.map((step) => (
                <div key={step.id} className="flex flex-col items-center gap-2">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 ${
                    currentStep >= step.id ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/20' : 'bg-accent text-muted-foreground'
                  }`}>
                    {step.icon}
                  </div>
                </div>
              ))}
            </div>
            <hr className="border-border/50" />
            <div className="text-center">
              <CardTitle className="text-2xl font-black uppercase tracking-tight">
                {currentStep === 1 && "Form 6: New Voter Enrollment"}
                {currentStep === 2 && "Constituency & Address"}
                {currentStep === 3 && "Biometric Authentication"}
                {currentStep === 4 && "Application Submitted"}
              </CardTitle>
              <CardDescription>
                {currentStep === 1 && "Enter your primary identity as per legal documents."}
                {currentStep === 2 && "Specify your Assembly and Parliamentary jurisdiction."}
                {currentStep === 3 && "Secure AI enrollment for zero-fraud election participation."}
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="min-h-[350px] flex flex-col justify-center py-8 px-10">
            <AnimatePresence mode="wait">
              {currentStep === 1 && (
                <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
                  <div className="space-y-2">
                    <Label>Full Name (as per Aadhaar)</Label>
                    <Input placeholder="Enter your full name" className="rounded-xl h-12" />
                  </div>
                  <div className="space-y-2">
                    <Label>Father's / Husband's Name</Label>
                    <Input placeholder="Enter relation's name" className="rounded-xl h-12" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Date of Birth</Label>
                      <Input type="date" className="rounded-xl h-12" />
                    </div>
                    <div className="space-y-2">
                      <Label>Gender</Label>
                      <Select>
                        <SelectTrigger className="rounded-xl h-12">
                          <SelectValue placeholder="Select" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="M">Male</SelectItem>
                          <SelectItem value="F">Female</SelectItem>
                          <SelectItem value="O">Third Gender</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Aadhaar Number</Label>
                    <div className="relative">
                       <IdCard className="absolute left-3 top-3.5 w-5 h-5 text-muted-foreground" />
                       <Input placeholder="XXXX XXXX XXXX" className="rounded-xl h-12 pl-10" />
                    </div>
                  </div>
                </motion.div>
              )}

              {currentStep === 2 && (
                 <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>State / UT</Label>
                            <Select>
                                <SelectTrigger className="rounded-xl h-12">
                                    <SelectValue placeholder="Select State" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="MH">Maharashtra</SelectItem>
                                    <SelectItem value="DL">Delhi</SelectItem>
                                    <SelectItem value="UP">Uttar Pradesh</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label>District</Label>
                            <Input placeholder="Enter District" className="rounded-xl h-12" />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <Label>Assembly Constituency (Vidhan Sabha)</Label>
                        <Input placeholder="e.g. Pune Cantonment" className="rounded-xl h-12" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>PIN Code</Label>
                            <Input placeholder="XXXXXX" className="rounded-xl h-12" />
                        </div>
                        <div className="space-y-2">
                            <Label>Taluk / Tehsil</Label>
                            <Input placeholder="Enter Taluk" className="rounded-xl h-12" />
                        </div>
                    </div>
                 </motion.div>
              )}

              {currentStep === 3 && (
                <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6 text-center">
                    <div className="flex flex-col items-center gap-4 py-8">
                        <div className="w-32 h-32 bg-primary/5 rounded-full flex items-center justify-center border-2 border-dashed border-primary/30 relative">
                           <ScanFace className="w-12 h-12 text-primary" />
                           <motion.div 
                                className="absolute inset-0 border-2 border-primary rounded-full"
                                animate={{ scale: [1, 1.1, 1], opacity: [1, 0, 1] }}
                                transition={{ duration: 2, repeat: Infinity }}
                           />
                        </div>
                        <p className="font-bold text-lg">AI Face Enrollment</p>
                        <p className="text-xs text-muted-foreground px-12">
                            Please look directly at the camera. This biometric template will be used for secure booth-level authentication.
                        </p>
                    </div>
                    <div className="p-4 bg-primary/5 border border-primary/20 rounded-2xl flex gap-3 text-left">
                        <ShieldCheck className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                        <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider">
                            DPDP Compliant Secure Biometric Storage
                        </p>
                    </div>
                </motion.div>
              )}

              {currentStep === 4 && (
                <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-12 space-y-6">
                    <div className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto shadow-xl shadow-green-500/20">
                       <CheckCircle2 className="w-10 h-10 text-white" />
                    </div>
                    <div className="space-y-2">
                        <h2 className="text-2xl font-black uppercase">Application Successful!</h2>
                        <p className="text-muted-foreground text-sm px-8">
                            Your Form 6 has been submitted. A Booth Level Officer (BLO) will visit your address for field verification.
                        </p>
                    </div>
                    <div className="bg-accent/30 p-6 rounded-3xl text-left border border-border/50">
                        <div className="flex justify-between items-center mb-4">
                            <span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Reference ID</span>
                            <span className="font-mono font-black text-primary">ECI-6692-X10-26</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Current Status</span>
                            <Badge className="bg-yellow-500 hover:bg-yellow-500 rounded-full px-4">BLO Assigned</Badge>
                        </div>
                    </div>
                </motion.div>
              )}
            </AnimatePresence>
          </CardContent>

          <CardFooter className="flex justify-between border-t border-border/50 bg-accent/20 py-8 px-10">
            {currentStep < 4 ? (
              <>
                <Button variant="ghost" onClick={() => currentStep > 1 && setCurrentStep(currentStep-1)} disabled={currentStep === 1} className="rounded-2xl px-6">
                  <ArrowLeft className="mr-2 w-4 h-4" /> Back
                </Button>
                <Button onClick={handleNext} disabled={loading} className="rounded-2xl px-10 shadow-xl shadow-primary/30 h-12 font-bold">
                  {currentStep === 3 ? "Submit Form 6" : "Next Phase"}
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </>
            ) : (
              <Link href="/" className="w-full">
                <Button className="w-full rounded-2xl py-6 text-lg font-bold">
                  Go to Home Page
                </Button>
              </Link>
            )}
          </CardFooter>
        </Card>
        
        <div className="mt-8 flex justify-center gap-8 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
            <Link href="#" className="hover:text-primary transition-colors">Voter Guidelines</Link>
            <Link href="#" className="hover:text-primary transition-colors">Privacy Policy</Link>
            <Link href="#" className="hover:text-primary transition-colors">Contact Helpdesk</Link>
        </div>
      </div>
    </div>
  )
}

export default Form6Registration
