import { useMutation, useQueryClient } from "@tanstack/react-query"
import { AxiosError } from "axios"
import { deleteBank } from "../../api/bank.api"


export const useDeleteBank = () => {
  const queryClient = useQueryClient()
  
  const mutation = useMutation<boolean, AxiosError, string>(
    {
      mutationFn: async (id: string) => {
        const res =  await deleteBank(id)
        queryClient.invalidateQueries({queryKey: ['bank']})
        return res
      },
    }
  )

  return mutation
}