/**
 * Auth API — login, refresh, MFA.
 */
import api from "@/lib/api-client";

export interface LoginResponse {
  access_token: string;
  token_type: string;
  refresh_token?: string;
  mfa_required: boolean;
  mfa_token?: string;
}

export interface MeResponse {
  id: string;
  email: string;
  full_name: string;
  role: string;
  scope_type: string | null;
  scope_id: string | null;
  is_active: boolean;
  is_verified: boolean;
}

/** OAuth2 password login */
export async function loginPassword(
  email: string,
  password: string
): Promise<LoginResponse> {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const { data } = await api.post<LoginResponse>("/login/access-token", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

/** TOTP verification after MFA prompt */
export async function verifyMfa(
  mfaToken: string,
  code: string
): Promise<LoginResponse> {
  const { data } = await api.post<LoginResponse>(
    `/login/verify-mfa?mfa_token=${encodeURIComponent(mfaToken)}&code=${code}`
  );
  return data;
}

/** Who am I? */
export async function getMe(): Promise<MeResponse> {
  const { data } = await api.get<MeResponse>("/users/me");
  return data;
}

/** Logout — clear tokens */
export function logout(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
