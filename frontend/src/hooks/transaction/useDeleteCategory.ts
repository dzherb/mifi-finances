import { useMutation, useQueryClient } from "@tanstack/react-query"
import { deleteTransactionCategory } from "../../api/transaction.api"
import { AxiosError } from "axios"


export const useDeleteCategory = () => {
  const queryClient = useQueryClient()
  
  const mutation = useMutation<boolean, AxiosError, string>(
    {
      mutationFn: async (id: string) => {
        const res =  await deleteTransactionCategory(id)
        queryClient.invalidateQueries({queryKey: ['transactionsCategories']})
        return res
      },
    }
  )

  return mutation
}