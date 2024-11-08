import { Link, useNavigate } from "react-router-dom"
import { useAppSelector, useAppDispatch } from "../../app/hooks"
import { selectSession } from "../../features/sessionSlice"
import { selectUserById } from "../../features/usersSlice"
import {
  Question,
  selectQuestionById,
  deleteOneQuestion,
} from "../../features/questionsSlice"
import { selectAnswerById, Answer } from "../../features/answersSlice"
import { RenderPost } from "./RenderPost"

const absurd = (input: never): never => input
type PostType =
  | {
      type: "question"
      post: Question
    }
  | {
      type: "answer"
      post: Answer
    }

interface Props {
  type: "question" | "answer"
  id: number
}
// Post renders top level question or answer
export const Post = ({ type, id }: Props) => {
  const returnQuestionOrAnswerPost = (
    type: "question" | "answer",
    id: number,
  ): PostType => {
    if (type === "question") {
      const post = useAppSelector(state => selectQuestionById(state, id))
      return { type: "question", post: post }
    } else if (type === "answer") {
      const post = useAppSelector(state => selectAnswerById(state, id))
      return { type: "answer", post: post }
    } else {
      return absurd(type)
    }
  }
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const post = returnQuestionOrAnswerPost(type, id)
  const { user } = useAppSelector(selectSession)
  const isUserPostWriter = user && user.id === post.post.user_id

  if (!post) {
    // return <div>Loading post...</div>
    return <></>
  }

  const getPermalinkTitle = (post: PostType) => {
    const permalinkBase = `${post.type}`
    if (post.type === "question") {
      const { post: question } = post
      return `${permalinkBase}-${question.id}-${question.title.replaceAll(" ", "-").slice(0, 20).toLowerCase()}`
    } else if (post.type === "answer") {
      return permalinkBase
    } else {
      const absurd = (input: never): never => input
      return absurd(post)
    }
  }

  const permalink = getPermalinkTitle(post)
  const postWriter = useAppSelector(state =>
    selectUserById(state, post.post.user_id),
  )

  const handleDeletePost = async (e: React.MouseEvent<HTMLButtonElement>) => {
    dispatch(deleteOneQuestion(id))
    navigate("/questions")
  }
  return (
    <div>
      <div className="question-body">
        <div>
          <div>Up</div>
          <div>{post.post.total_score}</div>
          <div>Down</div>
          <div>Save</div>
        </div>
        <div id={permalink}>
          <RenderPost postContent={post.post.content} />
          <div className="question-meta">
            <div>
              <a href={`#${permalink}`}>Share</a> |<button>Like post</button>
              {isUserPostWriter && <Link to={`edit`}>Edit {type}</Link>}
              {isUserPostWriter && (
                <button onClick={handleDeletePost}>Delete {type}</button>
              )}
            </div>
            <div>
              Posted by{" "}
              <a href={`/users/userId/username`}>{postWriter.username}</a>
            </div>
          </div>
          <div>Comments here</div>
        </div>
      </div>
    </div>
  )
}
