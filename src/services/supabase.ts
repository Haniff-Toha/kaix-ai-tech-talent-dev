import { createClient, SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

// Validate that Supabase is configured
const isConfigured = supabaseUrl.startsWith('http') && supabaseAnonKey.length > 10

let supabase: SupabaseClient

if (isConfigured) {
  supabase = createClient(supabaseUrl, supabaseAnonKey)
} else {
  console.warn(
    '⚠️ Supabase not configured. Fill VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in fe/.env'
  )
  // Create a dummy client that won't crash the app
  // Replace with real values when ready
  supabase = createClient('https://placeholder.supabase.co', 'placeholder-key')
}

export { supabase, isConfigured as isSupabaseConfigured }
