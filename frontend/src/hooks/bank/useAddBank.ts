import { useMutation, useQueryClient } from "@tanstack/react-query"
import { AxiosError } from "axios"
import { addBank } from "../../api/bank.api"


export const useAddBank = () => {
  const queryClient = useQueryClient()
  
  const mutation = useMutation<boolean, AxiosError, string>(
    {
      mutationFn: async (name: string) => {
        const res =  await addBank(name)
        queryClient.invalidateQueries({queryKey: ['bank']})
        return res
      },
    }
  )

  return mutation
}