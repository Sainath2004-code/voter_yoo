"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar, 
  MoreVertical, 
  Users, 
  CheckCircle2, 
  Clock,
  AlertCircle,
  ChevronRight,
  Settings2,
  Trash2,
  Eye
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'

const elections = [
  { id: 'EL-2026-001', title: 'General National Assembly Elections 2026', status: 'Ongoing', type: 'National', date: 'Oct 12, 2026', voters: '124.5M', progress: 68 },
  { id: 'EL-2026-002', title: 'State Legislative Council - Maharashtra', status: 'Draft', type: 'State', date: 'Nov 22, 2026', voters: '42.1M', progress: 0 },
  { id: 'EL-2025-098', title: 'Municipal Corporation Bye-Elections', status: 'Completed', type: 'Local', date: 'May 04, 2025', voters: '1.2M', progress: 100 },
  { id: 'EL-2026-003', title: 'State Legislative Council - Karnataka', status: 'Published', type: 'State', date: 'Dec 05, 2026', voters: '38.4M', progress: 0 },
]

const ElectionManagement = () => {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Election Management</h1>
          <p className="text-muted-foreground">Create, schedule, and monitor election cycles.</p>
        </div>
        <Dialog>
          <DialogTrigger asChild>
            <Button className="rounded-xl shadow-lg shadow-primary/20">
              <Plus className="w-4 h-4 mr-2" />
              Create Election
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>New Election Cycle</DialogTitle>
            </DialogHeader>
            <div className="grid gap-6 py-4">
              <div className="space-y-2">
                <Label htmlFor="title">Election Title</Label>
                <Input id="title" placeholder="e.g. General Assembly 2026" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="type">Type</Label>
                  <Input id="type" placeholder="National / State" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date">Start Date</Label>
                  <Input id="date" type="date" />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="desc">Description</Label>
                <textarea 
                  id="desc" 
                  className="w-full min-h-[100px] rounded-xl border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder="Enter election guidelines and details..."
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline">Cancel</Button>
              <Button>Create Draft</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <Card className="border-border/50 bg-background/50 overflow-hidden">
        <CardHeader className="border-b border-border/50 bg-accent/10">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="relative w-full md:w-96">
              <Search className="absolute left-3 top-2.5 w-4 h-4 text-muted-foreground" />
              <Input 
                placeholder="Search elections by title or ID..." 
                className="pl-10 rounded-xl bg-background"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="rounded-lg">
                <Filter className="w-4 h-4 mr-2" />
                Filters
              </Button>
              <Button variant="outline" size="sm" className="rounded-lg">
                Sort By
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-border/50 text-xs font-bold uppercase text-muted-foreground bg-accent/5">
                  <th className="px-6 py-4">Election Details</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Type</th>
                  <th className="px-6 py-4">Start Date</th>
                  <th className="px-6 py-4">Total Voters</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {elections.map((election) => (
                  <tr key={election.id} className="hover:bg-accent/30 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-bold text-sm">{election.title}</span>
                        <span className="text-xs text-muted-foreground font-mono">{election.id}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <Badge 
                        variant="secondary" 
                        className={cn(
                          "rounded-lg px-2.5 py-0.5 font-semibold",
                          election.status === 'Ongoing' && "bg-green-500/10 text-green-500",
                          election.status === 'Draft' && "bg-slate-500/10 text-slate-500",
                          election.status === 'Published' && "bg-blue-500/10 text-blue-500",
                          election.status === 'Completed' && "bg-primary/10 text-primary",
                        )}
                      >
                        {election.status === 'Ongoing' && <Clock className="w-3 h-3 mr-1" />}
                        {election.status === 'Completed' && <CheckCircle2 className="w-3 h-3 mr-1" />}
                        {election.status}
                      </Badge>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-medium">{election.type}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm">
                        <Calendar className="w-4 h-4 text-muted-foreground" />
                        {election.date}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm font-bold">
                        <Users className="w-4 h-4 text-muted-foreground font-normal" />
                        {election.voters}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon" className="rounded-lg">
                            <MoreVertical className="w-4 h-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-48 rounded-xl p-2">
                          <DropdownMenuItem className="rounded-lg gap-2 cursor-pointer">
                            <Eye className="w-4 h-4" /> View Details
                          </DropdownMenuItem>
                          <DropdownMenuItem className="rounded-lg gap-2 cursor-pointer">
                            <Settings2 className="w-4 h-4" /> Configuration
                          </DropdownMenuItem>
                          <DropdownMenuItem className="rounded-lg gap-2 cursor-pointer">
                            <Users className="w-4 h-4" /> Candidates
                          </DropdownMenuItem>
                          <hr className="my-1 border-border/50" />
                          <DropdownMenuItem className="rounded-lg gap-2 cursor-pointer text-red-500 focus:text-red-600 focus:bg-red-500/10">
                            <Trash2 className="w-4 h-4" /> Cancel Election
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-border/50 bg-primary/5 border-primary/20">
          <CardContent className="p-6 flex items-start gap-4">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary shrink-0">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold">Automated Auditing</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Real-time integrity checks are active for all ongoing elections. 
              </p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 bg-yellow-500/5 border-yellow-500/20">
          <CardContent className="p-6 flex items-start gap-4">
            <div className="p-3 bg-yellow-500/10 rounded-2xl text-yellow-600 shrink-0">
              <AlertCircle className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-yellow-700 dark:text-yellow-500">Resource Alert</h4>
              <p className="text-xs text-muted-foreground mt-1">
                2 Polling stations in Region X report high voter density.
              </p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/50 bg-blue-500/5 border-blue-500/20">
          <CardContent className="p-6 flex items-start gap-4">
            <div className="p-3 bg-blue-500/10 rounded-2xl text-blue-500 shrink-0">
              <Settings2 className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold">Next Phase Prep</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Candidate nomination starts for State Assembly in 48 hours.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

import { cn } from '@/lib/utils'

export default ElectionManagement
