import { useMutation, useQueryClient } from "@tanstack/react-query"
import { addTransaction, AddTransactionReq } from "../../api/transaction.api"
import { AxiosError } from "axios"


export const useAddTransaction = () => {
  const queryClient = useQueryClient()
  
  const mutation = useMutation<boolean, AxiosError, AddTransactionReq>(
    {
      mutationFn: async (options: AddTransactionReq) => {
        const res =  await addTransaction(options)
        queryClient.invalidateQueries({queryKey: ['transaction']})
        return res
      },
    }
  )

  return mutation
}