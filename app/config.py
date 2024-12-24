import os
import supabase

SUPABASE_URL = 'https://uriryzqzmddbshefzhjg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyaXJ5enF6bWRkYnNoZWZ6aGpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwMzIwNTQsImV4cCI6MjA0OTYwODA1NH0.kSnyjCwO7LJYz9kukcyje7eO5wZ_iYB_GBTty2NJqAU'
# Outras configurações (exemplo: debug mode, database URI)
DEBUG = True
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)