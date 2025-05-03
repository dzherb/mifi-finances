import { useQuery } from "@tanstack/react-query"
import { getTransactions, GetTransactionsReq } from "../../api/transaction.api"

export function useGetTransactions(options: GetTransactionsReq) {
  const {limit, offset, order_by} = options
  const response = useQuery({
    queryKey: ['transaction', limit, offset, order_by],
    queryFn: async () => {
      const transactions = await getTransactions(options)
      return transactions
    }
  })

  return response
}