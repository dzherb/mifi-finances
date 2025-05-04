import { useMutation, useQueryClient } from "@tanstack/react-query"
import { updateTransaction, UpdateTransactionReq } from "../../api/transaction.api"
import { AxiosError } from "axios"


export const useUpdateTransaction = () => {
  const queryClient = useQueryClient()

  const mutation = useMutation<boolean, AxiosError, UpdateTransactionReq>(
    {
      mutationFn: async (options: UpdateTransactionReq) => {
        const res =  await updateTransaction(options)
        queryClient.invalidateQueries({queryKey: ['transaction']})
        return res
      },
    }
  )

  return mutation
}