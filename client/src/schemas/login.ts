import z from 'zod'

export const loginSchema = z.object({
    username: z.string().min(1).max(100),
    password: z.string().min(1).max(100),
})

export type Login = z.infer<typeof loginSchema>