import { createClient } from 'npm:@supabase/supabase-js@2'

const allowedOrigins = new Set([
  'https://jun6954.github.io',
  'http://localhost:4173',
])

function corsHeaders(request: Request) {
  const origin = request.headers.get('origin') || ''
  return {
    'Access-Control-Allow-Origin': allowedOrigins.has(origin) ? origin : 'https://jun6954.github.io',
    'Access-Control-Allow-Headers': 'authorization, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    Vary: 'Origin',
  }
}

function response(request: Request, body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders(request), 'Content-Type': 'application/json' },
  })
}

Deno.serve(async request => {
  if (request.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders(request) })
  if (request.method !== 'POST') return response(request, { error: 'Method not allowed' }, 405)

  const sharedSecret = Deno.env.get('FAVORITES_SHARE_SECRET')
  const secretKeys = JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS') || '{}')
  const serviceKey = secretKeys.default || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
  if (!sharedSecret || !serviceKey) return response(request, { error: 'Server is not configured' }, 500)

  let payload: { token?: string; action?: string; projectKey?: string }
  try {
    payload = await request.json()
  } catch {
    return response(request, { error: 'Invalid request body' }, 400)
  }
  if (payload.token !== sharedSecret) return response(request, { error: 'Invalid access link' }, 403)

  const database = createClient(Deno.env.get('SUPABASE_URL')!, serviceKey)
  if (payload.action === 'list') {
    const { data, error } = await database.from('shared_favorites').select('project_key').order('created_at')
    if (error) return response(request, { error: 'Could not load favorites' }, 500)
    return response(request, { projectKeys: data.map(row => row.project_key) })
  }

  if (!payload.projectKey || !['add', 'remove'].includes(payload.action || '')) {
    return response(request, { error: 'Invalid favorite request' }, 400)
  }
  const { error } = payload.action === 'add'
    ? await database.from('shared_favorites').upsert({ project_key: payload.projectKey })
    : await database.from('shared_favorites').delete().eq('project_key', payload.projectKey)
  if (error) return response(request, { error: 'Could not save favorite' }, 500)
  return response(request, { ok: true })
})
