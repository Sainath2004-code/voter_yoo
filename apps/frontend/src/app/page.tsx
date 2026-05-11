"use client"

import React from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  ShieldCheck, 
  UserCheck, 
  BarChart3, 
  MapPin, 
  Fingerprint, 
  ScanFace,
  ChevronRight,
  Vote,
  Globe
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-primary rounded-lg">
              <Vote className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="font-bold text-xl tracking-tight hidden sm:block">National Voter Portal</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <Link href="#features" className="hover:text-primary transition-colors">Features</Link>
            <Link href="#stats" className="hover:text-primary transition-colors">Statistics</Link>
            <Link href="#about" className="hover:text-primary transition-colors">About</Link>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost" size="sm">Login</Button>
            </Link>
            <Link href="/register">
              <Button size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold px-6 shadow-lg shadow-primary/20">
                Register Now
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px]" />
          <div className="absolute bottom-[10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[120px]" />
        </div>

        <div className="container mx-auto px-4 relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-4xl mx-auto"
          >
            <Badge variant="outline" className="mb-4 py-1 px-4 border-primary/20 bg-primary/5 text-primary animate-pulse">
              Government-Grade Security
            </Badge>
            <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/60">
              The Future of Digital <span className="text-primary">Electoral Democracy</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
              Experience the world's most secure and transparent voter management platform powered by AI biometrics and blockchain-grade audit trails.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link href="/register">
                <Button size="lg" className="h-14 px-10 text-lg rounded-2xl shadow-xl shadow-primary/30 group">
                  Get Started 
                  <ChevronRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Button size="lg" variant="outline" className="h-14 px-10 text-lg rounded-2xl border-2">
                Live Election Stats
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature Cards */}
      <section id="features" className="py-24 bg-accent/30 relative">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <ScanFace className="w-8 h-8" />,
                title: "AI Face Verification",
                desc: "Enterprise-grade facial recognition with liveness detection to prevent identity fraud."
              },
              {
                icon: <Fingerprint className="w-8 h-8" />,
                title: "Biometric Auth",
                desc: "Secure fingerprint matching integrated with national identity databases."
              },
              {
                icon: <ShieldCheck className="w-8 h-8" />,
                title: "Immutable Audit",
                desc: "Every action is digitally signed and logged in an immutable audit infrastructure."
              },
              {
                icon: <MapPin className="w-8 h-8" />,
                title: "GIS Mapping",
                desc: "Real-time polling station locators and constituency boundary visualization."
              },
              {
                icon: <BarChart3 className="w-8 h-8" />,
                title: "Real-time Analytics",
                desc: "Live turnout monitoring and demographic analysis for election observers."
              },
              {
                icon: <Globe className="w-8 h-8" />,
                title: "Multi-Language",
                desc: "Full accessibility support with localized interfaces for all state regions."
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="bg-background/50 border-border/50 hover:border-primary/50 transition-all duration-300 hover:shadow-2xl hover:shadow-primary/5 h-full group">
                  <CardContent className="pt-8 px-8 pb-10">
                    <div className="p-3 rounded-2xl bg-primary/5 text-primary w-fit mb-6 group-hover:scale-110 transition-transform">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {feature.desc}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-border/50">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Vote className="w-6 h-6 text-primary" />
            <span className="font-bold text-lg">National Electoral Commission</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © 2026 National Electoral Voter Management System. Secure Government Infrastructure.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
