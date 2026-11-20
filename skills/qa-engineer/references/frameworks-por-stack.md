# Frameworks por stack

Exemplos de configuração e de teste por linguagem, usados pela skill `qa-engineer`.

### Node.js / TypeScript

**Unit + Integration:** Jest ou Vitest (prefira Vitest em projetos Vite/Next.js moderno)

```typescript
// jest.config.ts ou vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',        // 'jsdom' para componentes React
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      thresholds: { lines: 80, functions: 80, branches: 70 }
    }
  }
})
```

```typescript
// Exemplo: teste unitário bem estruturado
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { UserService } from './user.service'
import { UserRepository } from './user.repository'

describe('UserService', () => {
  let userService: UserService
  let userRepository: UserRepository

  beforeEach(() => {
    // Mock do repositório — isolamos a lógica de negócio do banco
    userRepository = {
      findByEmail: vi.fn(),
      save: vi.fn(),
    } as unknown as UserRepository
    userService = new UserService(userRepository)
  })

  describe('createUser', () => {
    it('deve criar usuário quando email ainda não existe', async () => {
      vi.mocked(userRepository.findByEmail).mockResolvedValue(null)
      vi.mocked(userRepository.save).mockResolvedValue({ id: '123', email: 'joao@email.com', name: 'João' })

      const result = await userService.createUser({ email: 'joao@email.com', name: 'João' })

      expect(result.id).toBe('123')
      expect(userRepository.save).toHaveBeenCalledOnce()
    })

    it('deve lançar erro quando email já está em uso', async () => {
      vi.mocked(userRepository.findByEmail).mockResolvedValue({ id: '999', email: 'joao@email.com', name: 'João' })

      await expect(
        userService.createUser({ email: 'joao@email.com', name: 'João' })
      ).rejects.toThrow('Email já está em uso')
    })
  })
})
```

**Integração de API com Supertest:**

```typescript
import request from 'supertest'
import { app } from '../app'
import { db } from '../database'

describe('POST /users', () => {
  beforeEach(async () => {
    await db.migrate.latest()
    await db.seed.run()
  })

  afterEach(async () => {
    await db.migrate.rollback()
  })

  it('deve retornar 201 e o usuário criado', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'novo@email.com', name: 'Novo Usuário' })
      .expect(201)

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: 'novo@email.com',
    })
  })

  it('deve retornar 409 quando email já existe', async () => {
    await request(app).post('/users').send({ email: 'existente@email.com', name: 'Teste' })

    await request(app)
      .post('/users')
      .send({ email: 'existente@email.com', name: 'Outro' })
      .expect(409)
  })
})
```

---

### Python

**Unit + Integration:** Pytest (sempre, não use unittest)

```python
# conftest.py — fixtures compartilhadas
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
```

```python
# test_user_service.py
from unittest.mock import MagicMock, patch
import pytest
from app.services.user_service import UserService

class TestCreateUser:
    def test_cria_usuario_quando_email_nao_existe(self):
        repo = MagicMock()
        repo.find_by_email.return_value = None
        repo.save.return_value = {"id": "123", "email": "joao@email.com"}

        service = UserService(repo)
        result = service.create_user(email="joao@email.com", name="João")

        assert result["id"] == "123"
        repo.save.assert_called_once()

    def test_levanta_erro_quando_email_ja_existe(self):
        repo = MagicMock()
        repo.find_by_email.return_value = {"id": "999"}

        service = UserService(repo)

        with pytest.raises(ValueError, match="Email já está em uso"):
            service.create_user(email="joao@email.com", name="João")
```

---

### E2E com Playwright (qualquer stack web)

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Autenticação', () => {
  test('usuário consegue fazer login com credenciais válidas', async ({ page }) => {
    await page.goto('/login')

    await page.getByLabel('Email').fill('usuario@teste.com')
    await page.getByLabel('Senha').fill('senha123')
    await page.getByRole('button', { name: 'Entrar' }).click()

    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('Bem-vindo')).toBeVisible()
  })

  test('exibe erro com credenciais inválidas', async ({ page }) => {
    await page.goto('/login')

    await page.getByLabel('Email').fill('errado@teste.com')
    await page.getByLabel('Senha').fill('senhaerrada')
    await page.getByRole('button', { name: 'Entrar' }).click()

    await expect(page.getByText('Credenciais inválidas')).toBeVisible()
    await expect(page).toHaveURL('/login')
  })
})
```

---

