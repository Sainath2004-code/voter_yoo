"use client";

/**
 * Dashboard home page — powered by real API data via React Query.
 * All metrics come from the analytics microservice.
 */
import { useQuery } from "@tanstack/react-query";
import { getNationalOverview, type NationalOverview } from "@/lib/analytics-api";
import { getMyGrievances } from "@/lib/grievance-api";
import { getMe } from "@/lib/auth-api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Users, Vote, AlertTriangle, CheckCircle2, Clock, TrendingUp } from "lucide-react";

function StatCard({
  label,
  value,
  icon: Icon,
  badge,
  loading,
}: {
  label: string;
  value?: number | string;
  icon: React.ElementType;
  badge?: string;
  loading?: boolean;
}) {
  return (
    <Card className="bg-background/60 border-border/50 hover:border-primary/30 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5">
      <CardContent className="pt-6 px-6 pb-6">
        <div className="flex items-start justify-between">
          <div className="p-2 rounded-xl bg-primary/10 text-primary">
            <Icon className="w-5 h-5" />
          </div>
          {badge && (
            <Badge variant="outline" className="text-[10px] border-green-500/30 text-green-500">
              {badge}
            </Badge>
          )}
        </div>
        <div className="mt-4">
          {loading ? (
            <Skeleton className="h-8 w-24 mb-1" />
          ) : (
            <p className="text-3xl font-bold tracking-tight">
              {typeof value === "number" ? value.toLocaleString("en-IN") : (value ?? "—")}
            </p>
          )}
          <p className="text-sm text-muted-foreground mt-1">{label}</p>
        </div>
      </CardContent>
    </Card>
  );
}

export default function DashboardPage() {
  const { data: me } = useQuery({
    queryKey: ["me"],
    queryFn: getMe,
    staleTime: 5 * 60 * 1000,
  });

  const {
    data: overview,
    isLoading: overviewLoading,
    isError: overviewError,
  } = useQuery<NationalOverview>({
    queryKey: ["national-overview"],
    queryFn: getNationalOverview,
    staleTime: 60 * 1000, // 1-min cache
  });

  const { data: myGrievances, isLoading: grievancesLoading } = useQuery({
    queryKey: ["my-grievances"],
    queryFn: getMyGrievances,
    staleTime: 30 * 1000,
  });

  const openGrievances = myGrievances?.filter(
    (g) => !["resolved", "closed"].includes(g.status)
  ).length;

  return (
    <div className="space-y-8">
      {/* Greeting */}
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">
          Welcome back{me?.full_name ? `, ${me.full_name.split(" ")[0]}` : ""}
        </h1>
        <p className="text-muted-foreground mt-1">
          {me?.role ?? "Voter"} — {me?.is_verified ? "Verified Account" : "Unverified"}
        </p>
      </div>

      {/* KPI Cards */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
        <StatCard
          label="Total Registered Voters"
          value={overview?.total_registered_voters}
          icon={Users}
          badge="National"
          loading={overviewLoading}
        />
        <StatCard
          label="Active Elections"
          value={overview?.active_elections}
          icon={Vote}
          loading={overviewLoading}
        />
        <StatCard
          label="Pending Grievances"
          value={overview?.pending_grievances}
          icon={AlertTriangle}
          loading={overviewLoading}
        />
        <StatCard
          label="My Open Grievances"
          value={openGrievances}
          icon={Clock}
          loading={grievancesLoading}
        />
      </section>

      {/* Application Funnel */}
      {(overviewLoading || overview?.application_funnel) && (
        <section>
          <h2 className="text-lg font-bold mb-4">Registration Pipeline</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {overviewLoading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <Card key={i} className="p-4">
                    <Skeleton className="h-6 w-12 mb-2" />
                    <Skeleton className="h-4 w-20" />
                  </Card>
                ))
              : Object.entries(overview!.application_funnel).map(([status, count]) => (
                  <Card
                    key={status}
                    className="p-4 bg-background/60 border-border/50 hover:border-primary/30 transition-all"
                  >
                    <p className="text-2xl font-bold">{Number(count).toLocaleString("en-IN")}</p>
                    <p className="text-xs text-muted-foreground mt-1 capitalize">
                      {status.replace(/_/g, " ")}
                    </p>
                  </Card>
                ))}
          </div>
        </section>
      )}

      {/* Error state */}
      {overviewError && (
        <Card className="border-red-500/30 bg-red-500/5 p-6">
          <p className="text-sm text-red-400">
            ⚠ Could not load national overview — analytics service may be offline.
          </p>
        </Card>
      )}

      {/* Recent Grievances mini-table */}
      {myGrievances && myGrievances.length > 0 && (
        <section>
          <h2 className="text-lg font-bold mb-4">My Grievances</h2>
          <div className="space-y-3">
            {myGrievances.slice(0, 5).map((g) => (
              <Card key={g.id} className="p-4 flex items-center justify-between bg-background/60 border-border/50">
                <div>
                  <p className="font-medium text-sm">{g.subject}</p>
                  <p className="text-xs text-muted-foreground capitalize mt-0.5">
                    {g.category.replace(/_/g, " ")} · Priority: {g.priority}
                  </p>
                </div>
                <Badge
                  variant="outline"
                  className={
                    g.status === "resolved" || g.status === "closed"
                      ? "border-green-500/30 text-green-500"
                      : "border-amber-500/30 text-amber-500"
                  }
                >
                  {g.status}
                </Badge>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
