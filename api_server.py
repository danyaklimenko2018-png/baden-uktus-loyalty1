import asyncio
import os
import sqlite3
from aiohttp import web

async def handle_api_user(request):
    try:
        user_id = request.query.get('user_id')
        if not user_id:
            return web.json_response({'error': 'No user_id'}, status=400)
        
        user_id = int(user_id)
        
        conn = sqlite3.connect('loyalty.db')
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, current_discount, current_month_visits FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return web.json_response({'error': 'User not found'}, status=404)
        
        return web.json_response({
            'full_name': user[0],
            'discount': user[1],
            'visits': user[2]
        })
        
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def start_web_server():
    app = web.Application()
    app.router.add_get('/api/user', handle_api_user)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    await site.start()
    print(f"Server started on port {port}")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_web_server())
