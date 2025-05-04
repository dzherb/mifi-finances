import { useQuery, UseQueryResult } from "@tanstack/react-query"
import { IOption } from "../../utils"
import { getBanks } from "../../api/bank.api"

export function useGetBanks(): UseQueryResult<IOption<number>[]> {
  const response = useQuery({
    queryKey: ['bank'],
    queryFn: async () => {
      const banks = await getBanks()
      return banks.map(bank => ({value: bank.id, label: bank.name}))
    }
  })

  return response
}