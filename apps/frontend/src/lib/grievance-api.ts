/**
 * Grievance API — submit, list mine, officer transition.
 */
import api from "@/lib/api-client";

export type GrievanceCategory =
  | "voter_registration"
  | "polling_booth"
  | "candidate_conduct"
  | "technical_issue"
  | "fraud_report";

export type GrievanceStatus =
  | "submitted"
  | "categorized"
  | "assigned"
  | "investigating"
  | "resolved"
  | "closed";

export interface GrievanceSubmitPayload {
  category: GrievanceCategory;
  subject: string;
  description: string;
  state_id: string;
  district_id?: string;
  ac_id?: string;
  priority?: "low" | "medium" | "high" | "emergency";
  attachment_urls?: string[];
}

export interface GrievanceSummary {
  id: string;
  category: GrievanceCategory;
  subject: string;
  status: GrievanceStatus;
  priority: string;
  sla_deadline: string;
  assigned_officer_id: string | null;
}

export async function submitGrievance(
  payload: GrievanceSubmitPayload
): Promise<{ id: string; status: GrievanceStatus; sla_deadline: string }> {
  const { data } = await api.post("/grievances", payload);
  return data;
}

export async function getMyGrievances(): Promise<GrievanceSummary[]> {
  const { data } = await api.get<GrievanceSummary[]>("/grievances/my");
  return data;
}

export async function transitionGrievance(
  grievanceId: string,
  newStatus: GrievanceStatus,
  notes?: string
): Promise<{ id: string; new_status: GrievanceStatus }> {
  const { data } = await api.post(`/grievances/${grievanceId}/transition`, {
    new_status: newStatus,
    notes,
  });
  return data;
}
