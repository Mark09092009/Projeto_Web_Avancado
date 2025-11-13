"""
Teste(s) para o app `gerenciamento`.

Este arquivo deve conter testes para as funcionalidades de estoque,
compras, vendas e financeiro. Use `django.test.TestCase` para testes que
precisem de acesso ao banco de dados de teste.

Exemplo mínimo:

	from django.urls import reverse

	class GerenciamentoSmokeTests(TestCase):
		def test_estoque_view_requires_login(self):
			resp = self.client.get(reverse('estoque_gasolina'))
			self.assertEqual(resp.status_code, 302)  # redireciona para login

"""

from django.test import TestCase

# Arquivo preparado para receber testes do app `gerenciamento`.
