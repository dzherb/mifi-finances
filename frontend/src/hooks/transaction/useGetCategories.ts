import { useQuery, UseQueryResult } from "@tanstack/react-query"
import { getTransactionsCategories } from "../../api/transaction.api"
import { IOption } from "../../utils"

export function useGetTransactionsCategories(): UseQueryResult<IOption<number>[]> {
  const response = useQuery({
    queryKey: ['transactionsCategories'],
    queryFn: async () => {
      const cats = await getTransactionsCategories()
      return cats.map(cat => ({value: cat.id, label: cat.name}))
    }
  })

  return response
}