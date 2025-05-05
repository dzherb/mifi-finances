import { useQuery } from "@tanstack/react-query"
import { GetDynamicByIntervalReq, getDynamicsByInterval } from "../../api/analytics"

export function useGetDynamicsByInterval(options: GetDynamicByIntervalReq) {
  const {start, end, interval} = options
  const response = useQuery({
    queryKey: ['analitics', start, end, interval],
    queryFn: async () => {
      const res = await getDynamicsByInterval(options)
      return [
        {
          label: 'DynamicsByInterval',
          data: res.entries
        }
      ]
    }
  })

  return response
}