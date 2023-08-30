import pytest

from langchain.chains.qa_with_sources.base import QAWithSourcesChain
from tests.unit_tests.llms.fake_llm import FakeLLM


@pytest.mark.parametrize(
    "text,answer,sources",
    [
        (
            "This Agreement is governed by English law.\nSOURCES: 28-pl",
            "This Agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "This Agreement is governed by English law.\nSources: 28-pl",
            "This Agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "This Agreement is governed by English law.\nsource: 28-pl",
            "This Agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "This Agreement is governed by English law.\nSource: 28-pl",
            "This Agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "According to the sources the agreement is governed by English law.\n"
            "Source: 28-pl",
            "According to the sources the agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "This Agreement is governed by English law.\n"
            "SOURCES: 28-pl\n\n"
            "QUESTION: Which state/country's law governs the interpretation of the "
            "contract?\n"
            "FINAL ANSWER: This Agreement is governed by English law.\n"
            "SOURCES: 28-pl",
            "This Agreement is governed by English law.\n",
            "28-pl",
        ),
        (
            "The president did not mention Michael Jackson in the provided content.\n"
            "SOURCES: \n\n"
            "Note: Since the content provided does not contain any information about "
            "Michael Jackson, there are no sources to cite for this specific question.",
            "The president did not mention Michael Jackson in the provided content.\n",
            "",
        ),
        # The following text was generated by gpt-3.5-turbo
        (
            "To diagnose the problem, please answer the following questions and send "
            "them in one message to IT:\nA1. Are you connected to the office network? "
            "VPN will not work from the office network.\nA2. Are you sure about your "
            "login/password?\nA3. Are you using any other VPN (e.g. from a client)?\n"
            "A4. When was the last time you used the company VPN?\n"
            "SOURCES: 1\n\n"
            "ALTERNATIVE OPTION: Another option is to run the VPN in CLI, but keep in "
            "mind that DNS settings may not work and there may be a need for manual "
            "modification of the local resolver or /etc/hosts and/or ~/.ssh/config "
            "files to be able to connect to machines in the company. With the "
            "appropriate packages installed, the only thing needed to establish "
            "a connection is to run the command:\nsudo openvpn --config config.ovpn"
            "\n\nWe will be asked for a username and password - provide the login "
            "details, the same ones that have been used so far for VPN connection, "
            "connecting to the company's WiFi, or printers (in the Warsaw office)."
            "\n\nFinally, just use the VPN connection.\n"
            "SOURCES: 2\n\n"
            "ALTERNATIVE OPTION (for Windows): Download the"
            "OpenVPN client application version 2.6 or newer from the official "
            "website: https://openvpn.net/community-downloads/\n"
            "SOURCES: 3",
            "To diagnose the problem, please answer the following questions and send "
            "them in one message to IT:\nA1. Are you connected to the office network? "
            "VPN will not work from the office network.\nA2. Are you sure about your "
            "login/password?\nA3. Are you using any other VPN (e.g. from a client)?\n"
            "A4. When was the last time you used the company VPN?\n",
            "1",
        ),
    ],
)
def test_spliting_answer_into_answer_and_sources(
    text: str, answer: str, sources: str
) -> None:
    qa_chain = QAWithSourcesChain.from_llm(FakeLLM())
    generated_answer, generated_sources = qa_chain._split_sources(text)
    assert generated_answer == answer
    assert generated_sources == sources
