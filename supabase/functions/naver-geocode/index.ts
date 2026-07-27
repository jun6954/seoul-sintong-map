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

  const clientId = Deno.env.get('NAVER_MAPS_CLIENT_ID')
  const clientSecret = Deno.env.get('NAVER_MAPS_CLIENT_SECRET')
  if (!clientId || !clientSecret) return response(request, { error: 'Geocoding is not configured' }, 500)

  let query = ''
  try {
    const payload = await request.json()
    query = String(payload.query || '').trim()
  } catch {
    return response(request, { error: 'Invalid request body' }, 400)
  }
  if (!query || query.length > 200) return response(request, { error: 'Invalid address query' }, 400)

  const endpoint = new URL('https://maps.apigw.ntruss.com/map-geocode/v2/geocode')
  endpoint.searchParams.set('query', query)
  endpoint.searchParams.set('count', '5')
  endpoint.searchParams.set('language', 'kor')
  try {
    const apiResponse = await fetch(endpoint, {
      headers: {
        Accept: 'application/json',
        'x-ncp-apigw-api-key-id': clientId,
        'x-ncp-apigw-api-key': clientSecret,
      },
    })
    const data = await apiResponse.json().catch(() => ({}))
    if (!apiResponse.ok || data.status !== 'OK') {
      console.error('Naver geocoding request failed', apiResponse.status)
      return response(request, { error: 'Geocoding request failed' }, 502)
    }
    return response(request, { addresses: data.addresses || [] })
  } catch (error) {
    console.error('Naver geocoding request failed', error)
    return response(request, { error: 'Geocoding request failed' }, 502)
  }
})
