import { useParams } from "react-router-dom"

import { Post } from "../Post/Post"

import "./Question.css"

export const QuestionMain = () => {
  const { questionId } = useParams()
  const questionIdNum = Number(questionId)
  // Select question details from store
  // const question = selectQuestion(questionId)
  // Select answerIds from store
  const answerIds: number[] = [1, 2, 3]
  return (
    <div>
      <h1 className="question-title">Question {questionId} title</h1>
      <Post type="question" id={questionIdNum} />
      <hr />
      <h1 className="answers-title">## Answers</h1>
      {answerIds.length > 0
        ? answerIds.map(answerId => {
            return (
              <>
                <Post key={answerId} type="answer" id={answerId} />
                <hr />
              </>
            )
          })
        : "No one answered yet"}
    </div>
  )
}
