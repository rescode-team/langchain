"""Test ChatFireworks wrapper."""

import pytest

from langchain.chat_models.fireworks import ChatFireworks
from langchain.schema import ChatGeneration, ChatResult, LLMResult
from langchain.schema.messages import BaseMessage, HumanMessage, SystemMessage


def test_chat_fireworks() -> None:
    """Test ChatFireworks wrapper."""
    chat = ChatFireworks()
    message = HumanMessage(content="What is the weather in Redwood City, CA today")
    response = chat([message])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_chat_fireworks_model() -> None:
    """Test ChatFireworks wrapper handles model_name."""
    chat = ChatFireworks(model="foo")
    assert chat.model == "foo"


def test_chat_fireworks_system_message() -> None:
    """Test ChatFireworks wrapper with system message."""
    chat = ChatFireworks()
    system_message = SystemMessage(content="You are to chat with the user.")
    human_message = HumanMessage(content="Hello")
    response = chat([system_message, human_message])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_chat_fireworks_generate() -> None:
    """Test ChatFireworks wrapper with generate."""
    chat = ChatFireworks(model_kwargs={"n": 2})
    message = HumanMessage(content="Hello")
    response = chat.generate([[message], [message]])
    assert isinstance(response, LLMResult)
    assert len(response.generations) == 2
    for generations in response.generations:
        assert len(generations) == 2
        for generation in generations:
            assert isinstance(generation, ChatGeneration)
            assert isinstance(generation.text, str)
            assert generation.text == generation.message.content


def test_chat_fireworks_multiple_completions() -> None:
    """Test ChatFireworks wrapper with multiple completions."""
    chat = ChatFireworks(model_kwargs={"n": 5})
    message = HumanMessage(content="Hello")
    response = chat._generate([message])
    assert isinstance(response, ChatResult)
    assert len(response.generations) == 5
    for generation in response.generations:
        assert isinstance(generation.message, BaseMessage)
        assert isinstance(generation.message.content, str)


def test_chat_fireworks_llm_output_contains_model_id() -> None:
    """Test llm_output contains model_id."""
    chat = ChatFireworks()
    message = HumanMessage(content="Hello")
    llm_result = chat.generate([[message]])
    assert llm_result.llm_output is not None
    assert llm_result.llm_output["model"] == chat.model


def test_fireworks_invoke() -> None:
    """Tests chat completion with invoke"""
    chat = ChatFireworks()
    result = chat.invoke("How is the weather in New York today?", stop=[","])
    assert isinstance(result.content, str)
    assert result.content[-1] == ","


@pytest.mark.asyncio
async def test_fireworks_ainvoke() -> None:
    """Tests chat completion with invoke"""
    chat = ChatFireworks()
    result = await chat.ainvoke("How is the weather in New York today?", stop=[","])
    assert isinstance(result.content, str)
    assert result.content[-1] == ","


def test_fireworks_batch() -> None:
    """Test batch tokens from ChatFireworks."""
    chat = ChatFireworks()
    result = chat.batch(
        [
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
        ],
        config={"max_concurrency": 5},
        stop=[","],
    )
    for token in result:
        assert isinstance(token.content, str)
        assert token.content[-1] == ","


@pytest.mark.asyncio
async def test_fireworks_abatch() -> None:
    """Test batch tokens from ChatFireworks."""
    chat = ChatFireworks()
    result = await chat.abatch(
        [
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
            "What is the weather in Redwood City, CA today",
        ],
        config={"max_concurrency": 5},
        stop=[","],
    )
    for token in result:
        assert isinstance(token.content, str)
        assert token.content[-1] == ","


def test_fireworks_streaming() -> None:
    """Test streaming tokens from Fireworks."""
    llm = ChatFireworks()

    for token in llm.stream("I'm Pickle Rick"):
        assert isinstance(token.content, str)


def test_fireworks_streaming_stop_words() -> None:
    """Test streaming tokens with stop words."""
    llm = ChatFireworks()

    last_token = ""
    for token in llm.stream("I'm Pickle Rick", stop=[","]):
        last_token = token.content
        assert isinstance(token.content, str)
    assert last_token[-1] == ","


@pytest.mark.asyncio
async def test_chat_fireworks_agenerate() -> None:
    """Test ChatFireworks wrapper with generate."""
    chat = ChatFireworks(model_kwargs={"n": 2})
    message = HumanMessage(content="Hello")
    response = await chat.agenerate([[message], [message]])
    assert isinstance(response, LLMResult)
    assert len(response.generations) == 2
    for generations in response.generations:
        assert len(generations) == 2
        for generation in generations:
            assert isinstance(generation, ChatGeneration)
            assert isinstance(generation.text, str)
            assert generation.text == generation.message.content


@pytest.mark.asyncio
async def test_fireworks_astream() -> None:
    """Test streaming tokens from Fireworks."""
    llm = ChatFireworks()

    last_token = ""
    async for token in llm.astream(
        "Who's the best quarterback in the NFL?", stop=[","]
    ):
        last_token = token.content
        assert isinstance(token.content, str)
    assert last_token[-1] == ","
