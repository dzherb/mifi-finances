import { withRetry } from "./axios"

export type Interval = "week" | "month" | "quarter" | "year"
export interface DynamicsByIntervalEntry {
  date: string
  count: number
}
export interface DynamicsByInterval {
  start: string
  end: string
  interval: Interval
  entries: DynamicsByIntervalEntry[]
}
export interface GetDynamicByIntervalReq {
  start: string
  end: string
  interval: Interval
}
export async function getDynamicsByInterval(options: GetDynamicByIntervalReq): Promise<DynamicsByInterval> {
    const res = await withRetry(async (instance) => {return instance.get('/analytics/dynamics_by_interval', {params: options})})
    return res.data
}