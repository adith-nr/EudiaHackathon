import { z } from 'zod';
import { AGENT_ROLES } from './constants.js';

export const agentPayloadSchema = z.object({
  role: z.enum(AGENT_ROLES),
  context: z.object({
    storeId: z.string(),
    currency: z.string().length(3),
  }),
  goals: z.array(z.string()).min(1),
  data: z.record(z.any()).optional(),
});

export default agentPayloadSchema;
