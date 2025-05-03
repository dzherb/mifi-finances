import { useMutation } from "@tanstack/react-query"
import { createTransactionCategory } from "../../api/transaction.api"


export const useCreateTransaction = () => {
  const mutation = useMutation(
    {
      mutationFn: async (name: string) => {
        const res =  await createTransactionCategory(name)
        return res
      },
    }
  )

  return mutation
}