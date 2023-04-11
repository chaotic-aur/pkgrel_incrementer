#!/usr/bin/env python
from fastapi import FastAPI
import aiosqlite
import os

app = FastAPI()

@app.get('/{pkgname}/{pkgver}/{deps}')
async def get_pkgrel(pkgname: str, pkgver: str, deps: str):
    async with aiosqlite.connect(os.path.join(os.getenv('DATA_DIR', './data'), 'pkgrel.db')) as db:
        await db.execute('CREATE TABLE IF NOT EXISTS pkgrel (pkgname TEXT, pkgver TEXT, deps TEXT, pkgrel INTEGER, PRIMARY KEY (pkgname, pkgver, deps))')
        await db.execute('CREATE TABLE IF NOT EXISTS pkgrel_latest (pkgname TEXT, pkgver TEXT, pkgrel INTEGER, PRIMARY KEY (pkgname, pkgver))')
        
        async with db.execute('SELECT pkgrel FROM pkgrel WHERE pkgname = ? AND pkgver = ? AND deps = ?', (pkgname, pkgver, deps)) as cursor:
            row = await cursor.fetchone()
        if row is not None:
            return row[0]
        
        await db.execute('INSERT INTO pkgrel_latest (pkgname, pkgver, pkgrel) VALUES (?, ?, 1) ON CONFLICT (pkgname, pkgver) DO UPDATE SET pkgrel = pkgrel + 1', (pkgname, pkgver))
        async with db.execute('SELECT pkgrel FROM pkgrel_latest WHERE pkgname = ? AND pkgver = ?', (pkgname, pkgver)) as cursor:
            row = await cursor.fetchone()
        assert row is not None
        pkgrel = row[0]

        await db.execute('INSERT INTO pkgrel (pkgname, pkgver, deps, pkgrel) VALUES (?, ?, ?, ?)', (pkgname, pkgver, deps, pkgrel))

        await db.commit()
        return pkgrel
