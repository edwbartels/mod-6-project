import { useState } from "react"
import { useAppSelector, useAppDispatch } from "../../app/hooks"
import { selectTags, getAllTags } from "../../features/tagsSlice"
import { TagTile } from "../Tag/TagTile"
import "../tag/devicon-base.css"
import "./AllTags.css"

export const AllTags = () => {
  const dispatch = useAppDispatch()
  const [isLoadedTags, setIsLoadedTags] = useState(false)
  if (!isLoadedTags) {
    dispatch(getAllTags())
    setIsLoadedTags(true)
  }
  const tagIds = Object.keys(useAppSelector(selectTags))
  return (
    <div>
      <h1 className="tag-title">All Tags</h1>
      <hr className="tag-line" />
      <div className="all-tags-list">
        {tagIds.map(tagId => (
          <TagTile key={tagId} tagId={Number(tagId)} />
        ))}
      </div>
    </div>
  )
}
