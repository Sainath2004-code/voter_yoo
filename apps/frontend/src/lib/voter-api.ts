/**
 * Voter API — registration forms, profile, EPIC status.
 */
import api from "@/lib/api-client";

export interface Form6Payload {
  first_name: string;
  last_name: string;
  father_name: string;
  date_of_birth: string;  // YYYY-MM-DD
  gender: string;
  aadhaar_last4: string;
  state_id: string;
  district_id: string;
  ac_id: string;
  booth_id: string;
  pincode: string;
  address_line1: string;
}

export interface ApplicationResponse {
  application_id: string;
  status: string;
  message: string;
}

export async function submitForm6(payload: Form6Payload): Promise<ApplicationResponse> {
  const { data } = await api.post<ApplicationResponse>("/forms/form-6", payload);
  return data;
}

export interface VoterProfile {
  id: string;
  epic_number: string | null;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  verification_status: string;
  state_id: string;
  district_id: string;
}

export async function getMyProfile(): Promise<VoterProfile | null> {
  try {
    const { data } = await api.get<VoterProfile>("/voters/me");
    return data;
  } catch {
    return null;
  }
}
