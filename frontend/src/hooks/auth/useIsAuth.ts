import { useQuery } from "@tanstack/react-query"
import { getUser } from "../../api/user.api"


export const useIsAuth = () => {
  const response = useQuery({
    queryKey: ['isAuth'],
    queryFn: async () => {
      let user = await getUser()
      if (!user) {
        user = await getUser()
      }

      return !!user
    }
  })

  return response
}