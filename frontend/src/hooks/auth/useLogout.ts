import { useMutation, useQueryClient } from "@tanstack/react-query"
import { logout } from "../../api/user.api"


export function useLogout() {
  const queryClient = useQueryClient()

  const mutation = useMutation(
    {
      mutationFn: async () => {
        const res = await logout()
        await queryClient.invalidateQueries()

        return res
      }
    }
  )

  return mutation
}