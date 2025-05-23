import { useQuery } from "@tanstack/react-query"
import { getUser } from "../../api/user.api"


export const useIsAuth = () => {
  const response = useQuery({
    queryKey: ['auth'],
    queryFn: async () => {
      let user = await getUser()
      return user !== undefined
    }
  })

  return response
}