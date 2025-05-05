import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createTransactionCategory } from "../../api/transaction.api"
import { AxiosError } from "axios"


export const useAddCategory = () => {
  const queryClient = useQueryClient()
  
  const mutation = useMutation<boolean, AxiosError, string>(
    {
      mutationFn: async (name: string) => {
        const res =  await createTransactionCategory(name)
        queryClient.invalidateQueries({queryKey: ['transactionsCategories']})
        return res
      },
    }
  )

  return mutation
}