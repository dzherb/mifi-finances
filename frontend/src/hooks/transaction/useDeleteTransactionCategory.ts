import { useMutation } from "@tanstack/react-query"
import { deleteTransactionCategory } from "../../api/transaction.api"


export const useDeleteTransactionCategory = () => {
  const mutation = useMutation(
    {
      mutationFn: async (id: string) => {
        const res =  await deleteTransactionCategory(id)
        return res
      },
    }
  )

  return mutation
}