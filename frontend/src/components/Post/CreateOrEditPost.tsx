import React, { useState, ReactNode } from "react"
import { useParams, useNavigate } from "react-router-dom"

import { RenderPost } from "./RenderPost"

import "./Post.css"

export const CreateOrEditPost = () => {
  const { questionId } = useParams()
  const navigate = useNavigate()
  const emptyForm = {
    title: "",
    body: "",
  }

  const selectQuestionDetails = (questionId: string | undefined) => {
    // Placeholder function, will replace with store slice selector
    if (questionId === undefined) return null
    return { title: "question title", body: "question body" }
  }
  const initialForm = selectQuestionDetails(questionId) ?? emptyForm
  const [form, setForm] = useState(initialForm)

  const handleChangeForm =
    (field: string) =>
    (e: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      setForm({ ...form, [field]: e.currentTarget.value })
      if (field === "body") {
        // setPreview(renderMdToNode(e.currentTarget.value))
      }
    }

  const handleSubmitForm = () => {
    navigate(`/questions/${questionId}`)
  }
  return (
    <div className="post">
      <h1>New Question</h1>
      <form onSubmit={handleSubmitForm}>
        <div>
          <label>
            <div>Title*</div>
            <input
              name="title"
              className="post-title-input"
              type="text"
              defaultValue={form.title}
              placeholder="Question title..."
              onChange={handleChangeForm("title")}
            />
          </label>
        </div>
        <div>
          <label>
            <div>Question*</div>
            <textarea
              className="post-body-textarea"
              // cols={80}
              rows={10}
              name="body"
              defaultValue={form.body}
              placeholder="Question body..."
              onChange={handleChangeForm("body")}
            />
          </label>
        </div>
        <button>Submit question</button>
        <button>Cancel</button>
      </form>

      <RenderPost postContent={form.body} />
    </div>
  )
}
