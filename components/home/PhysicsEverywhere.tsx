import PhysicsEverywhereView from "@/components/home/PhysicsEverywhereView";
import { getPhysicsAroundPosts } from "@/lib/blog";
import { vietnamDayIndex } from "@/lib/physics-around";

export default function PhysicsEverywhere() {
  const posts = getPhysicsAroundPosts();
  if (posts.length === 0) return null;
  return <PhysicsEverywhereView posts={posts} initialIndex={vietnamDayIndex() % posts.length} />;
}
