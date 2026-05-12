/**
 * Analytics API — national/state/district overviews, audit feed.
 * Backed by real SQL aggregation queries.
 */
import api from "@/lib/api-client";

const ANALYTICS = process.env.NEXT_PUBLIC_ANALYTICS_URL ?? "http://localhost:8003/api/v1";

export interface NationalOverview {
  total_registered_voters: number;
  gender_breakdown: Record<string, number>;
  application_funnel: Record<string, number>;
  active_elections: number;
  pending_grievances: number;
}

export interface StateSummary {
  state_id: string;
  total_voters: number;
  pending_verifications: number;
  approved_registrations: number;
  rejected_registrations: number;
}

export interface DistrictSummary {
  district_id: string;
  total_voters: number;
  grievance_count: number;
}

export interface AuditEntry {
  action: string;
  resource: string;
  actor_id: string;
  timestamp: string;
}

// Uses a separate base URL for the analytics microservice
import axios from "axios";
const analyticsClient = axios.create({ baseURL: ANALYTICS });
analyticsClient.interceptors.request.use((cfg) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export async function getNationalOverview(): Promise<NationalOverview> {
  const { data } = await analyticsClient.get<NationalOverview>("/analytics/national");
  return data;
}

export async function getStateSummary(stateId: string): Promise<StateSummary> {
  const { data } = await analyticsClient.get<StateSummary>(`/analytics/state/${stateId}`);
  return data;
}

export async function getDistrictSummary(districtId: string): Promise<DistrictSummary> {
  const { data } = await analyticsClient.get<DistrictSummary>(`/analytics/district/${districtId}`);
  return data;
}

export async function getAuditActivity(limit = 50): Promise<AuditEntry[]> {
  const { data } = await analyticsClient.get<AuditEntry[]>(`/analytics/audit-activity?limit=${limit}`);
  return data;
}
